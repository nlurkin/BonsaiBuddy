/**
 * 
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


/**
 * Serializer for Documents.  Recognized primitve fields:      * ``StringField``     * ``URLField``     * ``EmailField``     * ``IntField``     * ``LongField``     * ``FloatField``     * ``DecimalField``     * ``BooleanField``     * ``DateTimeField``     * ``ComplexDateTimeField``     * ``ObjectIdField``     * ``SequenceField`` (assumes it has integer counter)     * ``UUIDField``     * ``GeoPointField``     * ``GeoJsonBaseField`` (all those fields)     * ``DateField``  Compound fields: ``ListField`` and ``DictField`` are mapped to corresponding DRF fields, with respect to nested field specification.  The ``ReferenceField`` is handled like ``ForeignKey`` in DRF: there nested serializer autogenerated if serializer depth greater then 0, otherwise it\'s handled by it\'s own (results as ``str(id)``).  For ``EmbeddedDocumentField`` also nested serializer autogenerated for non-zero depth, otherwise it is skipped. TODO: THIS IS PROBABLY WRONG AND SHOULD BE FIXED.  Generic fields ``GenericReferenceField`` and ``GenericEmbeddedDocumentField`` are handled by their own with corresponding serializer fields.  Not well supported or untested:      ``FileField``     ``ImageField``     ``BinaryField``  All other fields are mapped to ``DocumentField`` and probably will work wrong.
 */
export interface PatchedBonsaiTechnique { 
    readonly id?: string;
    short_name?: string;
    display_name?: string;
    description?: string;
    category?: string;
    published?: boolean;
    sequence?: number;
}

